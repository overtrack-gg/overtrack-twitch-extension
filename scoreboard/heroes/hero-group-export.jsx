// Name: Export Layers Inside Selected Group.jsx
// Description: Photoshop script that separately saves top level layers inside the selected group.
// https://gist.github.com/joonaspaakko/013a223e94ba0fb9a2a0

#target photoshop

try {
    var doc = app.activeDocument;
    var docName = doc.name.split('.')[0];
}
catch (e) {
    alert( 'Open a document first...' );
}

function init() {

    var savefiles;

    dlg.g.saveAs.minimumSize.width = 463;
    dlg.btns.minimumSize.height = 142;


    dlg.btns.save.onClick = function(){
       savefiles = true;
       dlg.close();
       return savefiles;
    };

    dlg.show();

    if ( savefiles ){

        var getDestination = Folder.selectDialog( 'Select destination folder...', doc.saved ? doc.path : '' );
        var group = doc.activeLayer;
        
        var groupLength = group.layers.length;

        for( var i = 0 ; i < groupLength; i++ ){
            group.layers[i].visible = false;
        }

        for( var i = 0 ; i < groupLength; i++ ){

            var layer = group.layers[ i ];
            var layerName = group.layers[ i ].name;
            var layerIndex = i+1;

            layer.visible = true;

            save.file( dlg, doc, getDestination, layerIndex, layerName );

            layer.visible = false;

        }

        alert('Files Saved!');

    }

}

var save = {
    file: function( dlg, doc, getDestination, layerIndex, layerName ) {

        var saveOptions = {};
        var formats = ["psd", "pdf", "png", "jpg", "tiff"];

        for ( var i=0; i < formats.length; i++ ) {
            if ( dlg.g.saveAs[ formats[i] ].value ) {

                var fileformat = formats[i];

                var path = getDestination + "/" + fileformat;

                makeFolder( path );

                doc.saveAs( File( path + "/" + dlg.g.filename.filename.text + layerName ), save[fileformat](), true );

            }
        }

    },
    psd: function() {

        var psd_saveOpts = new PhotoshopSaveOptions();

        psd_saveOpts.layers = true;
        psd_saveOpts.embedColorProfile = true;
        psd_saveOpts.annotations = true;
        psd_saveOpts.alphaChannels = true;

        return psd_saveOpts;

    },
    pdf: function() {

        var presetName = '[High Quality Print]';

        var pdf_SaveOpts = new PDFSaveOptions();

        pdf_SaveOpts.pDFPreset = presetName;

        return pdf_SaveOpts;

    },
    jpg: function() {

        var jpg_SaveOpts = new JPEGSaveOptions();

        jpg_SaveOpts.matte = MatteType.WHITE;
        jpg_SaveOpts.quality = 10;
        jpg_SaveOpts.formatOptions.STANDARDBASELINE;

        return jpg_SaveOpts;

    },
    png: function() {

        var png_SaveOpts = new PNGSaveOptions();

        png_SaveOpts.compression = 9;
        png_SaveOpts.interlaced = false;

        return png_SaveOpts;

    },
    tiff: function() {

        var tiff_SaveOpts = new TiffSaveOptions();

        tiff_SaveOpts.alphaChannels = true;
        tiff_SaveOpts.annotations = true;
        tiff_SaveOpts.imageCompression = TIFFEncoding.JPEG;
        tiff_SaveOpts.interleaveChannels = true;
        tiff_SaveOpts.jpegQuality = 10;
        tiff_SaveOpts.layers = true;
        tiff_SaveOpts.layerCompression = LayerCompression.ZIP;
        tiff_SaveOpts.transparency = true;

        return tiff_SaveOpts;

    }
};

// Prepare dialog...
var dlg = new Window("dialog {  \
    text: 'Export layers inside the selected group', \
    alignChildren:['left','center'], \
    orientation: 'row', \
    g: Group { \
        orientation:'column', \
        alignChildren: ['left','center'], \
        filename: Panel { \
            orientation:'column', \
            alignChildren: ['left','top'], \
            filename_text: StaticText { alignment:'left', text: 'Filename ( Incremental numbers added automatically ): '}, \
            filename: EditText { alignment:'left', preferredSize: [430,20], text: '"+ docName +"', active: true },  \
        }, \
        saveAs: Panel { \
            margins: 20, \
            spacing: 20, \
            orientation: 'row', \
            alignChildren: ['left','top'], \
            saveAs_txt: StaticText { text: 'Save as: '}, \
            jpg: Checkbox { text: 'jpg', value: false }, \
            psd: Checkbox { text: 'psd', value: false }, \
            pdf: Checkbox { text: 'pdf', value: false }, \
            png: Checkbox { text: 'png', value: true }, \
            tiff: Checkbox { text: 'tiff', value: false } \
        } \
    }, \
    btns: Panel { \
        margins: 20, \
        spacing: 20, \
        orientation: 'column',  \
        alignment: ['right','top'], \
        save: Button { text: 'Save', properties:{ name: 'ok' }, preferredSize:[88, 24] }, \
        cancel: Button { text: 'Cancel', properties:{ name: 'cancel' }, preferredSize:[88, 24] }, \
    } \
}");

function makeFolder( path ) {

    var newFolder = Folder( path );
    if( !newFolder.exists ) newFolder.create();

}

if ( app.documents.length > 0 ) {
    if ( app.activeDocument.activeLayer.layers ) {

            init();

    }
    else {
        alert( "Error: \nSelect a parent group of the layers you want to export.")
    }
}
