
from torch import nn
import torch.nn.functional as F



class Model(nn.Module):

    def __init__(self):
        """
        In the constructor we instantiate two nn.Linear module
        """
        super(Model, self).__init__()
        # self.l1 = nn.Linear(3000, 300)
        # self.l2 = nn.Linear(300, 10)

        self.l1 = nn.Linear(3000,1000 )
        self.l2 = nn.Linear(1000,10)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        In the forward function we accept a Variable of input data and we must return
        a Variable of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Variables.
        """
        out1 = F.relu(self.l1(x))
        y_pred = self.sigmoid(self.l2(out1))
        return y_pred
