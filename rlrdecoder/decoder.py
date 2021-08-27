from bitstring import ConstBitStream

from .utils import Size, read_str
from .replay import Replay
from .header_properties import HeaderProperties, Properties
from .net_cache import NetCache
from .errors import ReplayDecodingError


class ReplayDecoder:
    """
    This class provides logic for decoding a Rocket League replay file
    """

    def __init__(self) -> None:
        """
        Create a ReplayDecoder object. The constructor takes no arguments.
        To decode a replay, call :function:`decode_replay`
        """
        self.path = None
        self.replay = None
        self.bitstream = None
        self.netstream = None
        self.header_raw = None
        self.body_raw = None
        self.verbose = None

    def decode_replay(self, path: str, verbose: int = 0) -> Replay:
        """
        Decode a Rocket League replay file

        Attributes
        ----------
        path : str
            The replay file path
        verbose : int, optional
            Verbosity level (default=0)

        Returns
        -------
        :class:`Replay`
            a Replay object containing information decoded from the replay file
        """

        if not path.endswith('.replay'):
            # Not a replay file
            raise ValueError('Can only decode Rocket League .replay files')

        self.verbose = verbose
        self.path = path
        self.replay = Replay()
        self.bitstream = ConstBitStream(filename=self.path)
        self.__log(f'Attempting to decode {self.path}...', 1)
        try:
            self.decode_header()
            self.decode_body()
        except:
            raise ReplayDecodingError('Could not decode this replay file')
        self.__log(f'Successfully decoded {self.path}!', 1)
        return self.replay

    def decode_header(self):
        self.__log('Decoding header segment...', 1)
        self.replay.header_size = self.bitstream.read(Size.UINT32_LE)
        self.replay.header_crc = self.bitstream.read(Size.UINT32_LE)
        self.__log(f'Decoded header description: size={self.replay.header_size}, '
                   f'CRC={self.replay.header_crc}', 2)
        self.replay.engine_version = self.bitstream.read(Size.UINT32_LE)
        self.replay.licensee_version = self.bitstream.read(Size.UINT32_LE)
        if self.replay.engine_version > 865 and self.replay.licensee_version > 17:
            # Older replays won't have this segment
            self.replay.network_version = self.bitstream.read(
                Size.UINT32_LE)
        self.__log('Decoded version info', 2)
        self.__log(f'Replay Version info: engine_version={self.replay.engine_version}, '
                   f'licensee_version={self.replay.licensee_version}, '
                   f'network_version={self.replay.network_version}', 2)
        self.replay.game_type = read_str(self.bitstream)
        self.__log('Decoding header properties...', 1)
        self.replay.header_properties = HeaderProperties(
            self.decode_properties())
        self.__log('Successfully decoded header segment!', 1)

    def decode_properties(self):
        header_properties = {}
        while True:
            key, value = self.decode_property()
            if key:
                header_properties[key] = value
            else:
                return header_properties

    def decode_property(self):
        key = read_str(self.bitstream)
        if key == Properties.NONE:
            return None, None
        property_type = read_str(self.bitstream)
        self.__log(
            f'Decoding property of type {property_type} for key {key}...', 2)
        self.bitstream.read(Size.UINT64_LE)  # Ignore these 8 bytes
        value = None
        if property_type == Properties.BOOL_PROPERTY:
            value = self.bitstream.read(Size.BYTE).uint == 1
        elif property_type == Properties.BYTE_PROPERTY:
            value_type = read_str(self.bitstream)
            if value_type in ('OnlinePlatform_Steam', 'OnlinePlatform_PS4'):
                # If first string read is any of these, don't read a second string
                value = value_type
            else:
                value = {value_type: read_str(self.bitstream)}
        elif property_type == Properties.FLOAT_PROPERTY:
            value = self.bitstream.read(Size.FLOAT32_LE)
        elif property_type == Properties.INT_PROPERTY:
            value = self.bitstream.read(Size.INT32_LE)
        elif property_type == Properties.NAME_PROPERTY:
            value = read_str(self.bitstream)
        elif property_type == Properties.STR_PROPERTY:
            value = read_str(self.bitstream)
        elif property_type == Properties.QWORD_PROPERTY:
            value = self.bitstream.read(Size.INT64_LE)
        elif property_type == Properties.ARRAY_PROPERTY:
            arr_length = self.bitstream.read(Size.UINT32_LE)
            value = [self.decode_properties()
                     for _ in range(arr_length)]
        self.__log(f'Decoded property: key={key}, value={value}', 2)
        return key, value

    def decode_body(self):
        self.__log('Decoding body segment...', 1)
        self.replay.body_size = self.bitstream.read(Size.UINT32_LE)
        self.replay.body_crc = self.bitstream.read(Size.UINT32_LE)
        self.__log('Decoded body description (size/CRC)', 2)

        num_levels = self.bitstream.read(Size.UINT32_LE)
        self.replay.levels = [read_str(self.bitstream)
                              for _ in range(num_levels)]

        num_kf = self.bitstream.read(Size.UINT32_LE)
        self.replay.keyframes = [{
            'Time': self.bitstream.read(Size.FLOAT32_LE),
            'Frame': self.bitstream.read(Size.UINT32_LE),
            'Position': self.bitstream.read(Size.INT32_LE)} for _ in range(num_kf)]

        self.replay.network_size = self.bitstream.read(Size.UINT32_LE)
        self.netstream = self.bitstream.read(self.replay.network_size*8)

        num_debugs = self.bitstream.read(Size.UINT32_LE)
        self.replay.debug_logs = [{
            'Frame': self.bitstream.read(Size.INT32_LE),
            'User': read_str(self.bitstream),
            'Text': read_str(self.bitstream)} for _ in range(num_debugs)]

        num_tickmarks = self.bitstream.read(Size.UINT32_LE)
        self.replay.tickmarks = [{
            'Description': read_str(self.bitstream),
            'Frame': self.bitstream.read(Size.INT32_LE)} for _ in range(num_tickmarks)]

        num_packages = self.bitstream.read(Size.UINT32_LE)
        self.replay.packages = [read_str(self.bitstream)
                                for _ in range(num_packages)]

        num_objects = self.bitstream.read(Size.UINT32_LE)
        self.replay.objects = [
            read_str(self.bitstream) for _ in range(num_objects)]

        num_names = self.bitstream.read(Size.UINT32_LE)
        self.replay.names = [read_str(self.bitstream)
                             for _ in range(num_names)]

        num_maps = self.bitstream.read(Size.UINT32_LE)
        self.replay.class_map = {}
        for _ in range(num_maps):
            self.replay.class_map[self.bitstream.read(
                Size.INT32_LE)] = read_str(self.bitstream)

        num_net_caches = self.bitstream.read(Size.UINT32_LE)
        self.replay.net_caches = []
        for i in range(num_net_caches):
            cache = NetCache()
            cache.object_index = self.bitstream.read(Size.UINT32_LE)
            cache.parent_id = self.bitstream.read(Size.UINT32_LE)
            cache.cache_id = self.bitstream.read(Size.UINT32_LE)
            num_properties = self.bitstream.read(Size.UINT32_LE)
            cache.properties = [{
                'ObjectIndex': self.bitstream.read(Size.UINT32_LE),
                'StreamID': self.bitstream.read(Size.UINT32_LE)}
                for _ in range(num_properties)]
            cache.children = []
            cache.children_ids = []
            self.replay.net_caches.append(cache)
            for parent_cache in self.replay.net_caches[:-1]:
                if cache.parent_id == parent_cache.cache_id:
                    cache.parent = parent_cache
                    parent_cache.children.append(cache)
                    parent_cache.children_ids.append(cache.cache_id)
                    break
            if not cache.parent:
                cache.is_root = True
        self.__log('Successfully decoded body segment!', 1)

    def __log(self, message: str, lvl: int):
        # Send Verbose logs
        if self.verbose >= lvl:
            print(f'[ReplayDecoder] {message}')


def decode_replay(path: str, verbose: int = 0) -> Replay:
    """
    Decodes the Rocket League replay file at path

    Parameters
    ----------
    path : str
        The path of the replay file to decode
    verbose : int, optional
            Verbosity level (default=0)

    Returns
    -------
    :class:`Replay`
        a :class:`Replay` object storing all of the decoded data

    """

    decoder = ReplayDecoder()
    replay = decoder.decode_replay(path, verbose=verbose)
    return replay
