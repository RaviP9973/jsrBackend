require("dotenv").config();
const axios = require("axios");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const {imageUpload} = require("../controllers/imageUpload")

exports.genrateImage = async (req, res) => {
  try {

    // Ensure a file was uploaded
    if (!req.file) {
      return res.status(400).send("No image file uploaded!");
    }

    // Get the file path from the uploaded file
    const imagePath = req.file.path;

    // Read the image file as base64
    const imageBase64 = fs.readFileSync(imagePath, { encoding: "base64" });

    const pythonScriptPath = "processImg.py";
    const pythonProcess = spawn("python", [
      pythonScriptPath,
      imagePath,
    ]);

    let scriptOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      // console.log(data);
      scriptOutput += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python Error: ${data.toString()}`);
    });
    pythonProcess.on("close", async (code) => {
      if (code === 0) {
        try {
          // Parse the Python script output as JSON
          const result = JSON.parse(scriptOutput);

          // Define the path to the segmented image file
          const segmentedImagePath = path.join(__dirname, '../..', result.segmented_image_path);


          res.status(200).json({
            message: "Image processed and uploaded to cloudinary successfully!",
            result,
          });
        } catch (error) {
          console.error("Error parsing script output:", error.message);
          res.status(500).send("Failed to process the image output");
        }
      } else {
        console.error(`Python script exited with code ${code}`);
        res.status(500).send("An error occurred while processing the image");
      }
    });
  } catch (error) {
    console.error("Error processing the image:", error.message);
    res.status(500).send("An error occurred while processing the image");
  }
};
