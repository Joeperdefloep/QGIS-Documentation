"""
Model exported as python.
Name : rasterize_like
Group : 
With QGIS : 32211
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class Rasterize_like(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('reference', 'reference', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('vector', 'vector', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('field', 'field', type=QgsProcessingParameterField.Any, parentLayerParameterName='vector', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('rasterized', 'rasterized', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        reference = self.parameterAsRasterLayer(parameters, "reference", context)

        # Rasterize (vector to raster)
        alg_params = {
            'BURN': 0,
            'DATA_TYPE': 5,  # Float32
            'EXTENT': parameters['reference'],
            'EXTRA': '',
            'FIELD': parameters['field'],
            'HEIGHT': reference.rasterUnitsPerPixelY(),
            'INIT': None,
            'INPUT': parameters['vector'],
            'INVERT': False,
            'NODATA': -999,
            'OPTIONS': '',
            'UNITS': 1,  # Georeferenced units
            'USE_Z': False,
            'WIDTH': reference.rasterUnitsPerPixelX(),
            'OUTPUT': parameters['rasterized']
        }
        outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        feedback.pushInfo(str(outputs['RasterizeVectorToRaster']))
        results['Out'] = outputs['RasterizeVectorToRaster']['OUTPUT']
        return results

    def name(self):
        return 'rasterize_like'

    def displayName(self):
        return 'rasterize_like'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Rasterize_like()
