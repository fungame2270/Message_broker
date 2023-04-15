class CDProtoBadFormat(Exception):
    #Exception when source message is not CDProto.

    def __init__(self, original_msg: bytes=None) :
        #Store original message that triggered exception.
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        #Retrieve original message as a string.
        return self._original.decode("utf-8")