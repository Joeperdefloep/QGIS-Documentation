"""
Model exported as python.
Name : model
Group : 
With QGIS : 32212
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterDefinition
import processing

from pathlib import Path

class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('reference', 'reference', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('vector', 'vector', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('rasterizefields', 'rasterize fields', type=QgsProcessingParameterField.Any, parentLayerParameterName='vector', allowMultiple=True, defaultValue=None, defaultToAllFields=True))
        param = QgsProcessingParameterNumber('nodatavalue', 'nodata value', type=QgsProcessingParameterNumber.Double, defaultValue=-999)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterFolderDestination('outputfolder', 'Output folder'))
        self.addParameter(QgsProcessingParameterBoolean('loadoutputlayers', 'Load output layers', defaultValue=True))
        self.addParameter(QgsProcessingParameterRasterDestination('Rasterized', 'rasterized', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        reference = self.parameterAsRasterLayer(parameters, 'reference', context)
        fields = self.parameterAsFields(parameters, 'rasterizefields', context)
        out_dir = self.parameterAsString(parameters, 'outputfolder', context)
        
        for index, field in enumerate(fields):
            if not "OUT_FOLDER" in out_dir: #OUT_FOLDER
                out_path = Path(out_dir) / f'{field}_rasterized.tif'
            else:
                out_path = 'TEMPORARY_OUTPUT'

            # Rasterize (vector to raster)
            alg_params = {
                'BURN': 0,
                'DATA_TYPE': 5,  # Float32
                'EXTENT': parameters['reference'],
                'EXTRA': '',
                'FIELD': field,
                'HEIGHT': reference.rasterUnitsPerPixelY(),
                'INIT': None,
                'INPUT': parameters['vector'],
                'INVERT': False,
                'NODATA': parameters['nodatavalue'],
                'OPTIONS': '',
                'UNITS': 1,  # Georeferenced units
                'USE_Z': False,
                'WIDTH': reference.rasterUnitsPerPixelX(),
                'OUTPUT': parameters['Rasterized']
            }
            outputs['RasterizeVectorToRaster'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['Rasterized'] = outputs['RasterizeVectorToRaster']['OUTPUT']
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
