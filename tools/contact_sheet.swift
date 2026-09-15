// Contact sheets for video files, no ffmpeg needed (uses macOS AVFoundation).
// One row per clip, FRAMES evenly spaced thumbnails, ROWS clips per sheet.
//
// usage: swift tools/contact_sheet.swift <out_dir> <video> [<video> ...]
// env:   FRAMES (default 8), ROWS (default 6)
//
// Use camera proxies: small files, fast to decode.
import AVFoundation
import AppKit

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else {
    print("usage: swift contact_sheet.swift <out_dir> <video> [<video> ...]")
    exit(1)
}
let outDir = URL(fileURLWithPath: args[0])
let videos = args.dropFirst().map { URL(fileURLWithPath: $0) }.sorted { $0.lastPathComponent < $1.lastPathComponent }
let env = ProcessInfo.processInfo.environment
let frames = Int(env["FRAMES"] ?? "") ?? 8
let rowsPerSheet = Int(env["ROWS"] ?? "") ?? 6
let cellW = 256, cellH = 144, labelH = 18, gap = 4
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

struct Row {
    let name: String
    let duration: Double
    let shots: [(image: CGImage?, time: Double)]
}

func grab(_ url: URL) async -> Row {
    let asset = AVURLAsset(url: url)
    let duration = (try? await asset.load(.duration).seconds) ?? 0
    let gen = AVAssetImageGenerator(asset: asset)
    gen.appliesPreferredTrackTransform = true
    gen.maximumSize = CGSize(width: cellW, height: cellH)
    let tolerance = CMTime(seconds: 0.5, preferredTimescale: 600)
    gen.requestedTimeToleranceBefore = tolerance
    gen.requestedTimeToleranceAfter = tolerance
    var shots: [(image: CGImage?, time: Double)] = []
    for i in 0..<frames {
        let t = duration * (Double(i) + 0.5) / Double(frames)
        let image = try? await gen.image(at: CMTime(seconds: t, preferredTimescale: 600)).image
        shots.append((image, t))
    }
    return Row(name: url.lastPathComponent, duration: duration, shots: shots)
}

func draw(_ rows: [Row], to file: URL) {
    let width = gap + frames * (cellW + gap)
    let rowH = labelH + cellH + gap
    let height = gap + rows.count * rowH
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height, bitsPerSample: 8,
                               samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
                               bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
    let ctx = NSGraphicsContext.current!.cgContext
    NSColor(white: 0.1, alpha: 1).setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    let attrs: [NSAttributedString.Key: Any] = [
        .font: NSFont.monospacedSystemFont(ofSize: 12, weight: .semibold),
        .foregroundColor: NSColor.white,
    ]
    for (r, row) in rows.enumerated() {
        let top = height - gap - r * rowH  // CoreGraphics origin is bottom-left
        for (c, shot) in row.shots.enumerated() {
            let x = gap + c * (cellW + gap)
            if let image = shot.image {
                let scale = min(Double(cellW) / Double(image.width), Double(cellH) / Double(image.height))
                let w = Double(image.width) * scale, h = Double(image.height) * scale
                let rect = CGRect(x: Double(x) + (Double(cellW) - w) / 2, y: Double(top - labelH - cellH) + (Double(cellH) - h) / 2,
                                  width: w, height: h)
                ctx.draw(image, in: rect)
            }
            let label = c == 0
                ? String(format: "%@ %.0fs | %.1fs", row.name, row.duration, shot.time)
                : String(format: "%.1fs", shot.time)
            (label as NSString).draw(at: NSPoint(x: x + 2, y: top - labelH + 3), withAttributes: attrs)
        }
    }
    NSGraphicsContext.restoreGraphicsState()
    try? rep.representation(using: .jpeg, properties: [.compressionFactor: 0.75])?.write(to: file)
}

var rows: [Row] = []
for video in videos {
    rows.append(await grab(video))
}
var sheet = 1
for start in stride(from: 0, to: rows.count, by: rowsPerSheet) {
    let file = outDir.appendingPathComponent(String(format: "sheet_%02d.jpg", sheet))
    draw(Array(rows[start..<min(start + rowsPerSheet, rows.count)]), to: file)
    print(file.path)
    sheet += 1
}
