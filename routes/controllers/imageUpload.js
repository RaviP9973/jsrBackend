const cloudinary = require("cloudinary").v2

async function uploadFileToCloudinary(file,folder,quality){
    // const options = {folder};
    const options = { folder, resource_type: "auto" };
    console.log("inside the uploading function")
    if(quality){
        options.quality = quality;
    }
    return await cloudinary.uploader.upload(file.tempFilePath,options);
 }

 exports.imageUpload = async (req,res)=>{
    try {
        const file = req.files.imageFile;

        

        //file format supported
        // temp file empty h 
        const response = await uploadFileToCloudinary(file,"myfolder");
        console.log(response);
        //db me entry save krni h 
        const fileData = await  File.create({
            imageUrl:response.secure_url,
        })
        
        res.json({
            success:true,
            imageUrl:response.secure_url,
            message:'Image Successfully Uploaded'
        })
    } catch (error) {
        console.error(error);
        res.status(400).json({
            success:false,
            message:'Something went wrong'
        })
    }
 }