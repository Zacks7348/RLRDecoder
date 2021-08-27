from bitstring import ConstBitStream

from .utils import Size, read_str

class Properties:
    BOOL_PROPERTY = 'BoolProperty'
    BYTE_PROPERTY = 'ByteProperty'
    FLOAT_PROPERTY = 'FloatProperty'
    INT_PROPERTY = 'IntProperty'
    NAME_PROPERTY = 'NameProperty'
    STR_PROPERTY = 'StrProperty'
    QWORD_PROPERTY = 'QWordProperty'
    ARRAY_PROPERTY = 'ArrayProperty'
    NONE = 'None'

class HeaderProperties:
    def __init__(self, properties: dict) -> None:
        self.data = properties

    # Expose common properties for ease of use
    @property
    def team_size(self):
        return self.data.get('TeamSize')
    
    @property
    def team_0_score(self):
        return self.data.get('Team0Score')
    
    @property
    def team_1_score(self):
        return self.data.get('Team1Score')
    
    @property
    def goals(self):
        return self.data.get('Goals')
    
    @property
    def player_stats(self):
        return self.data.get('PlayerStats')
    
    @property
    def date(self):
        return self.data.get('Date')

    @property
    def num_frames(self):
        return self.data.get('NumFrames')
    
    @property
    def match_type(self):
        return self.data.get('MatchType')
    
    @property
    def max_channels(self):
        return self.data.get('MaxChannels')