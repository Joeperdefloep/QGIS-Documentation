"""
Model exported as python.
Name : Batch rasterize
Group : 
With QGIS : 31611
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterBoolean
import processing


class BatchRasterize(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                "likeraster", "like raster", defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "vector",
                "vector",
                types=[QgsProcessing.TypeVectorPolygon],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                "Fieldstorasterize",
                "Fields to rasterize",
                type=QgsProcessingParameterField.Numeric,
                parentLayerParameterName="vector",
                allowMultiple=True,
                defaultValue=None,
                defaultToAllFields=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                "Loadoutputlayers", "Load output layers", defaultValue=True
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        likeraster = self.parameterAsRasterLayer(parameters, "likeraster", context)

        # Rasterize (vector to raster)
        alg_params = {
            "BURN": 0,
            "DATA_TYPE": 5,
            "EXTENT": likeraster.extent(),
            "EXTRA": "",
            "FIELD": parameters["Fieldstorasterize"],
            "HEIGHT": likeraster.rasterunitsPerPixelY(),
            "INIT": None,
            "INPUT": parameters["vector"],
            "INVERT": False,
            "NODATA": 0,
            "OPTIONS": "",
            "UNITS": 1,
            "WIDTH": likeraster.rasterunitsPerPixelX(),
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["RasterizeVectorToRaster"] = processing.run(
            "gdal:rasterize",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        return results

    def name(self):
        return "Batch rasterize"

    def displayName(self):
        return "Batch rasterize"

    def group(self):
        return ""

    def groupId(self):
        return ""

    def createInstance(self):
        return BatchRasterize()
