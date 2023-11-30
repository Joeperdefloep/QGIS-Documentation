"""
Model exported as python.
Name : model
Group : 
With QGIS : 32212
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterDefinition
import processing


class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('vector', 'vector', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('rasterizefield', 'rasterize field', type=QgsProcessingParameterField.Any, parentLayerParameterName='vector', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('raster', 'reference', defaultValue=None))
        param = QgsProcessingParameterNumber('nodatavalue', 'nodata value', type=QgsProcessingParameterNumber.Double, defaultValue=-999)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterRasterDestination('Output', 'output', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        raster = self.parameterAsRasterLayer(parameters, 'raster', context)

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 0,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': parameters['raster'],
            'EXTRA': '',
            'FIELD': parameters['rasterizefield'],
            'HEIGHT': raster.rasterUnitsPerPixelY(),
            'INIT': None,
            'INPUT': parameters['vector'],
            'INVERT': False,
            'NODATA': parameters['nodatavalue'],
            'OPTIONS': '',
            'UNITS': 1,  # Georeferenced units
            'USE_Z': False,
            'WIDTH': raster.rasterUnitsPerPixelX(),
            'OUTPUT': parameters['Output']
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['RasterizeVectorToRaster']['OUTPUT']
        return results

    def name(self):
        return 'model'

    def displayName(self):
        return 'model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()
