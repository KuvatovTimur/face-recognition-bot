from dataclasses import dataclass

from dataclasses import dataclass


@dataclass
class FaceLocation:
    top: int
    right: int
    bottom: int
    left: int

    def to_dict(self):
        return {
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
            "left": self.left
        }
