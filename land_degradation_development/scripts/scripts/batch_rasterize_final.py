import os

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFolderDestination,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingUtils,
    QgsProject,
    QgsRasterLayer,
)

import processing


class Batch_raster(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    FIELDS = "FIELDS"
    OUT_FOLDER = "OUT_FOLDER"
    LOAD_OUTPUTS = "LOAD_OUTPUTS"

    final_layers = {}
    load_outputs = True

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                "likeraster", "like raster", defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(self.INPUT, "vector", defaultValue=None)
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELDS,
                "fields to select",
                type=0,
                allowMultiple=True,
                defaultToAllFields=True,
                parentLayerParameterName=self.INPUT,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                "VERBOSE_LOG", "Verbose logging", optional=True, defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(self.OUT_FOLDER, "Output directory")
        ),
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_OUTPUTS,
                "Load output layers?",
                optional=True,
                defaultValue=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        results = {}
        outputs = {}

        likeraster = self.parameterAsRasterLayer(parameters, "likeraster", context)
        vector = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        fields = self.parameterAsFields(parameters, self.FIELDS, context)
        out_dir = self.parameterAsString(parameters, self.OUT_FOLDER, context)
        load = self.parameterAsBool(parameters, "LOAD_OUTPUTS", context)
        if not load:
            self.load_outputs = False

        for index, field in enumerate(fields):
            if feedback.isCanceled():
                break
            feedback.pushInfo(str(field))
            if not "OUT_FOLDER" in out_dir:
                out_path = os.path.join(out_dir, f"{field}_rasterized.tif")
            else:
                out_path = "TEMPORARY_OUTPUT"

            # Rasterize (vector to raster)
            alg_params = {
                "BURN": 0,
                "DATA_TYPE": 5,
                "EXTENT": likeraster.extent(),
                "EXTRA": "",
                "FIELD": field,
                "INIT": None,
                "INPUT": parameters[self.INPUT],
                "INVERT": False,
                "NODATA": 0,
                "OPTIONS": "",
                "UNITS": 1,
                "OUTPUT": f"{field}",
                "HEIGHT": likeraster.rasterUnitsPerPixelY(),
                "WIDTH": likeraster.rasterUnitsPerPixelX(),
                "OUTPUT": out_path,
            }

            outputs[f"RasterizeVectorToRaster{field}"] = processing.run(
                "gdal:rasterize",
                alg_params,
                is_child_algorithm=True,
                context=context,
                feedback=feedback,
            )

            results[f"Raster_out{field}"] = outputs[f"RasterizeVectorToRaster{field}"][
                "OUTPUT"
            ]
            if out_path == "TEMPORARY_OUTPUT":
                self.final_layers[field] = QgsProcessingUtils.mapLayerFromString(
                    outputs[f"RasterizeVectorToRaster{field}"]["OUTPUT"], context
                )
            else:
                self.final_layers[
                    f"file_{index}"
                ] = QgsProcessingUtils.mapLayerFromString(
                    outputs[f"RasterizeVectorToRaster{field}"]["OUTPUT"], context
                )
            pcnt = int(index / len(fields) * 100)
            feedback.setProgress(pcnt)
        return results

    ######################################################################
    def postProcessAlgorithm(self, context, feedback):
        if self.load_outputs:
            for name, layer in self.final_layers.items():
                if layer.name() == "OUTPUT":
                    layer.setName(f"{name}_rasterized")
                QgsProject.instance().addMapLayer(layer)
        else:
            self.load_outputs = True
        self.final_layers.clear()
        return {}

    ######################################################################

    def name(self):
        return "Batch_rasterize_fields"

    def displayName(self):
        return "Batch_rasterize_fields"

    def group(self):
        return ""

    def groupId(self):
        return ""

    def createInstance(self):
        return Batch_raster()
