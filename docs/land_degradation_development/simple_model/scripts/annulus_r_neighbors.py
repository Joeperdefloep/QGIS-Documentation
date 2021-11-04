"""
Model exported as python.
Name : annulus mask for r.neighbours
Group : 
With QGIS : 32200
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFileDestination
import processing

from numpy import sqrt, fromfunction, logical_and, savetxt

class AnnulusMaskForRneighbours(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('innerradius', 'inner radius', type=QgsProcessingParameterNumber.Integer, minValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('outerradius', 'outer radius', type=QgsProcessingParameterNumber.Integer, minValue=2, defaultValue=3))
        self.addParameter(QgsProcessingParameterFileDestination('outfile', 'annular mask'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(0, model_feedback)
        
        r_in = self.parameterAsInt(parameters, 'innerradius', context)
        r_out = self.parameterAsInt(parameters, 'outerradius', context)
        
        outloc = self.parameterAsString(parameters, 'outfile', context) #+ ".txt"
        
        d = sqrt(fromfunction(lambda x,y: (x-r_out)**2+(y-r_out)**2,(2*r_out+1,2*r_out+1)))
        m = logical_and(d>=r_in, d<r_out)
        feedback.pushInfo(str(m))
        savetxt(outloc,m,fmt="%d")
        
        results = {}
        outputs = {}

        return results

    def name(self):
        return 'annulus mask for r.neighbours'

    def displayName(self):
        return 'annulus mask for r.neighbours'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return AnnulusMaskForRneighbours()
