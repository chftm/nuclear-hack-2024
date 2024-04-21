import 'dart:async';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:file_picker/file_picker.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Video Canvas',
      theme: ThemeData(
        primaryColor: const Color(0xFF0A0A0A),
        canvasColor: const Color(0xFF0A0A0A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
        ),
        textTheme: TextTheme(
          bodyText1: TextStyle(
              fontFamily: 'Jura',
              fontSize: 16.0 + 3,
              fontWeight: FontWeight.w500),
          bodyText2: TextStyle(
              fontFamily: 'Jura',
              fontSize: 14.0 + 3,
              fontWeight: FontWeight.w500),
          headline1: TextStyle(
              fontFamily: 'Jura',
              fontSize: 96.0 + 3,
              fontWeight: FontWeight.w500),
          headline2: TextStyle(
              fontFamily: 'Jura',
              fontSize: 60.0 + 3,
              fontWeight: FontWeight.w500),
          headline3: TextStyle(
              fontFamily: 'Jura',
              fontSize: 48.0 + 3,
              fontWeight: FontWeight.w500),
          headline4: TextStyle(
              fontFamily: 'Jura',
              fontSize: 34.0 + 3,
              fontWeight: FontWeight.w500),
          headline5: TextStyle(
              fontFamily: 'Jura',
              fontSize: 24.0 + 3,
              fontWeight: FontWeight.w500),
          headline6: TextStyle(
              fontFamily: 'Jura',
              fontSize: 20.0 + 3,
              fontWeight: FontWeight.w500),
          subtitle1: TextStyle(
              fontFamily: 'Jura',
              fontSize: 16.0 + 3,
              fontWeight: FontWeight.w500),
          subtitle2: TextStyle(
              fontFamily: 'Jura',
              fontSize: 14.0 + 3,
              fontWeight: FontWeight.w500),
          button: TextStyle(
              fontFamily: 'Jura',
              fontSize: 14.0 + 3,
              fontWeight: FontWeight.w500),
          caption: TextStyle(
              fontFamily: 'Jura',
              fontSize: 12.0 + 3,
              fontWeight: FontWeight.w500),
          overline: TextStyle(
              fontFamily: 'Jura',
              fontSize: 10.0 + 3,
              fontWeight: FontWeight.w500),
        ),
      ),
      home: const MyHomePage(title: 'Video Canvas Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Map<String, Rectangle> rectangles = {};
  Uint8List? _image;
  ui.Image? _backgroundImage;
  String? _videoPath;
  String? _backgroundImagePath;

  void addRectangle(Rectangle rectangle) {
    setState(() {
      rectangles[rectangle.name] = rectangle;
    });
  }


  Future getVideoPath() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.video,
    );

    if (result != null) {
      final file = result.files.single;
      if (kIsWeb) {
        // On web, the `path` property is always `null`. Use `bytes` instead.
        print('Video selected with ${file.bytes?.length} bytes');
      } else {
        print('Video path: ${file.path}');
        _videoPath = file.path; // Add this line
      }
      print('Video path: $_videoPath'); // Add this line
    } else {
      print('No video selected.');
    }
  }

  void exportRectangles(List<Rectangle> rectangles) {
    // Print the width and height of the image
    Map<String, String?> paths = {
      'backgroundImagePath': _backgroundImagePath,
      'videoPath': _videoPath,
    };
    if (_backgroundImage != null) {
      print('Image width: ${_backgroundImage!.width}');
      print('Image height: ${_backgroundImage!.height}');
    }

    // Print the list of rectangles with their names and corner coordinates
    for (var rectangle in rectangles) {
      print('Rectangle name: ${rectangle.name}');
      print('Top left corner: (${rectangle.start.dx}, ${rectangle.start.dy})');
      print('Bottom right corner: (${rectangle.end.dx}, ${rectangle.end.dy})');
    }
  }

  Future getImage() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.image,
    );

    if (result != null) {
      final file = result.files.single;
      if (kIsWeb) {
        // On web, the `path` property is always `null`. Use `bytes` instead.
        setState(() {
          _image = file.bytes;
        });
      } else {
        final fileBytes = await File(file.path!).readAsBytes();
        setState(() {
          _image = fileBytes;
          _backgroundImagePath = file.path; // Add this line
        });
      }

      if (_image != null) {
        _backgroundImage = await _loadImage(_image!);
      }
      print('Image path: $_backgroundImagePath'); // Add this line
    } else {
      print('No image selected.');
    }
  }

  Future<ui.Image> _loadImage(Uint8List img) async {
    final Completer<ui.Image> completer = Completer();
    ui.decodeImageFromList(img, (ui.Image image) {
      print('Image loaded successfully'); // Add this line
      return completer.complete(image);
    });
    return completer.future;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Row(
        children: [
          Expanded(
            flex: 1, // Make the list take up 1/5 of the screen
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20.0, 20.0, 20.0, 20.0),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.1),
                  border: Border.all(
                      color: Colors.white,
                      width: 1.0), // Make the background a little lighter
                  borderRadius: BorderRadius.circular(10.0),
                ),
                child: ListView.builder(
                  itemCount: rectangles.length,
                  itemBuilder: (context, index) {
                    var rectangleEntry = rectangles.entries.elementAt(index);
                    return ListTile(
                      title: Text(
                        rectangleEntry.key,
                        style: TextStyle(
                            color: Colors.white), // Make the text white
                      ),
                      subtitle: Text(
                        'Top Left: (${rectangleEntry.value.start.dx}, ${rectangleEntry.value.start.dy}), '
                        'Bottom Right: (${rectangleEntry.value.end.dx}, ${rectangleEntry.value.end.dy})',
                        style: TextStyle(
                            color: Colors.white), // Make the text white
                      ),
                    );
                  },
                ),
              ),
            ),
          ),
          Expanded(
            flex: 4, // Make the canvas take up the remaining 4/5 of the screen
            child: Stack(
              children: [
                CanvasWidget(
                    rectangles: rectangles.values.toList(),
                    onRectangleDrawn: addRectangle,
                    backgroundImage: _backgroundImage), // Add this line
              ],
            ),
          ),
        ],
      ),
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: getImage,
            backgroundColor: Colors.white,
            foregroundColor: const Color(0xFF0A0A0A),
            tooltip: 'Upload',
            child: const Icon(Icons.upload),
          ),
          SizedBox(width: 10), // Add some space between the buttons
          FloatingActionButton(
            onPressed: () {
              exportRectangles(rectangles.values.toList());
            },
            backgroundColor: Colors.white,
            foregroundColor: const Color(0xFF0A0A0A),
            tooltip: 'Export',
            child: const Icon(Icons.save),
          ),
          SizedBox(width: 10), // Add some space between the buttons
          FloatingActionButton(
            onPressed: getVideoPath,
            backgroundColor: Colors.white,
            foregroundColor: const Color(0xFF0A0A0A),
            tooltip: 'Import Video',
            child: const Icon(Icons.video_library),
          ),
        ],
      ),
    );
  }
}



class Rectangle {
  final Offset start;
  final Offset end;
  final String name;

  Rectangle({required this.start, required this.end, required this.name});
}

class CanvasWidget extends StatefulWidget {
  final List<Rectangle> rectangles;
  final Function(Rectangle) onRectangleDrawn;
  final ui.Image? backgroundImage; // Add this line

  CanvasWidget({required this.rectangles, required this.onRectangleDrawn, this.backgroundImage}); // Modify this line

  @override
  _CanvasWidgetState createState() => _CanvasWidgetState();
}

class _CanvasWidgetState extends State<CanvasWidget> {
  Offset? start;
  Offset? end;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanStart: (details) {
        setState(() {
          start = details.localPosition;
        });
      },
      onPanUpdate: (details) {
        setState(() {
          end = details.localPosition;
        });
      },
      onPanEnd: (details) {
        showDialog(
          context: context,
          builder: (context) {
            return AlertDialog(
              title: Text('Enter a name for this rectangle'),
              content: TextField(
                onSubmitted: (value) {
                  widget.onRectangleDrawn(
                      Rectangle(start: start!, end: end!, name: value));
                  Navigator.of(context).pop();
                },
              ),
            );
          },
        );
      },
      child: CustomPaint(
        size: Size.infinite,
        painter: RectanglePainter(
            rectangles: widget.rectangles,
            start: start,
            end: end,
            backgroundImage: widget.backgroundImage), // Add this line
      ),
    );
  }
}



class RectanglePainter extends CustomPainter {
  final List<Rectangle> rectangles;
  final Offset? start;
  final Offset? end;
  final ui.Image? backgroundImage; // Add this line

  RectanglePainter(
      {required this.rectangles,
        this.start,
        this.end,
        this.backgroundImage});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFF0F0F0)
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    final radius = Radius.circular(8.0); // Adjust for desired roundness

    if (backgroundImage != null) {// Add this line
      // Define the source rectangle as the entire image
      final srcRect = Offset.zero & Size(backgroundImage!.width.toDouble(), backgroundImage!.height.toDouble());

      // Calculate the scaling factors for width and height
      final scaleX = size.width / srcRect.width;
      final scaleY = size.height / srcRect.height;

      // Use the smaller of the two scaling factors to maintain aspect ratio
      final scale = scaleX < scaleY ? scaleX : scaleY;

      // Calculate the new width and height
      final newWidth = srcRect.width * scale;
      final newHeight = srcRect.height * scale;

      // Define the destination rectangle
      final dstRect = Offset.zero & Size(newWidth, newHeight);

      // Draw the image on the canvas, scaling and positioning it correctly
      canvas.drawImageRect(backgroundImage!, srcRect, dstRect, paint);
    }

    rectangles.forEach((rectangle) {
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromPoints(rectangle.start, rectangle.end),
          radius,
        ),
        paint,
      );

      textPainter.text = TextSpan(
        text: rectangle.name,
        style: TextStyle(color: Colors.black, backgroundColor: Colors.white),
      );

      textPainter.layout();

      textPainter.paint(
        canvas,
        Offset(
            rectangle.start.dx + 5, rectangle.end.dy - textPainter.height - 5),
      );
    });

    if (start != null && end != null) {
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromPoints(start!, end!),
          radius,
        ),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}

