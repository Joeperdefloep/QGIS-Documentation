"""
Model exported as python.
Name : model
Group : 
With QGIS : 32212
"""

from pathlib import Path

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProject
from qgis.core import QgsProcessingUtils
import processing


class BatchRasterizeLike(QgsProcessingAlgorithm):
    final_layers = {}
    load_outputs = True

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer("vector", "vector", defaultValue=None)
        )
        self.addParameter(
            QgsProcessingParameterField(
                "rasterizefield",
                "rasterize field",
                type=QgsProcessingParameterField.Any,
                parentLayerParameterName="vector",
                allowMultiple=True,
                defaultValue=None,
                defaultToAllFields=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer("raster", "reference", defaultValue=None)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                "loadoutputs", "Load output layers", defaultValue=True
            )
        )
        param = QgsProcessingParameterNumber(
            "nodatavalue",
            "nodata value",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=-999,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(
            QgsProcessingParameterFolderDestination("outputfolder", "Output folder")
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        raster = self.parameterAsRasterLayer(parameters, "raster", context)
        fields = self.parameterAsFields(parameters, "rasterizefield", context)
        out_dir = self.parameterAsString(parameters, "outputfolder", context)
        Path(out_dir).mkdir(exist_ok=True)

        self.load_outputs = self.parameterAsBool(parameters, "loadoutputs", context)

        for field in fields:
            out_path = str(Path(out_dir) / f"{field}_rasterized.tif")

            if model_feedback.isCanceled():
                break
            model_feedback.pushInfo("rasterizing for:" + str(field))

            # Rasterize (vector to raster)
            alg_params = {
                "BURN": 0,
                "DATA_TYPE": 5,  # Float32
                "EXTENT": parameters["raster"],
                "EXTRA": "",
                "FIELD": field,
                "HEIGHT": raster.rasterUnitsPerPixelY(),
                "INIT": None,
                "INPUT": parameters["vector"],
                "INVERT": False,
                "NODATA": parameters["nodatavalue"],
                "OPTIONS": "",
                "UNITS": 1,  # Georeferenced units
                "USE_Z": False,
                "WIDTH": raster.rasterUnitsPerPixelX(),
                "OUTPUT": out_path,
            }
            outputs[f"RasterizeVectorToRaster{field}"] = processing.run(
                "gdal:rasterize",
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )
            results[f"Raster_out{field}"] = outputs[f"RasterizeVectorToRaster{field}"][
                "OUTPUT"
            ]
            self.final_layers[field] = QgsProcessingUtils.mapLayerFromString(
                results[f"Raster_out{field}"], context
            )
        return results

    def postProcessAlgorithm(self, context, feedback):
        if not self.load_outputs:
            self.final_layers.clear()
            return {}

        for name, layer in self.final_layers.items():
            if layer.name() == "OUTPUT":
                layer.setName(f"{name}_rasterized")
            QgsProject.instance().addMapLayer(layer)
        self.final_layers.clear()
        return {}

    def name(self):
        return "batchrasterizelike"

    def displayName(self):
        return "Batch rasterize like"

    def group(self):
        return ""

    def groupId(self):
        return ""

    def createInstance(self):
        return BatchRasterizeLike()
