from dataclasses import dataclass


from dataclasses import dataclass


@dataclass
class FaceLocation:
    left_bottom_x: float
    left_bottom_y: float
    right_top_x: float
    right_top_y: float

    def to_dict(self):
        return {
            'left_bottom_x': self.left_bottom_x,
            'left_bottom_y': self.left_bottom_y,
            'right_top_x': self.right_top_x,
            'right_top_y': self.right_top_y
        }
