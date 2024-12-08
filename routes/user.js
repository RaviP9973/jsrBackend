const express = require("express");
const { genrateImage } = require("./controllers/genrateImage");
const upload = require("../middlewares/multer")
const Router = express.Router();

Router.post("/genrateImage",upload.single('image'),genrateImage)
module.exports = Router;