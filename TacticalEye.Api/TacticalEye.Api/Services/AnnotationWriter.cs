using System.IO;
using System.Text;
using System.Threading.Tasks;
using TacticalEye.Api.Models;

namespace TacticalEye.Api.Services
{
    public class AnnotationWriter : IAnnotationWriter
    {
        // Target points to the valid execution path of the local Counter-Strike 2 directory tree
        private const string OutputPath = @"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\annotations\local\tactical_nodes.txt";

        public async Task WriteNativeAnnotationFileAsync(LineupModel activeLineup)
        {
            var contentBuilder = new StringBuilder();

            contentBuilder.AppendLine("kv3_annotations");
            contentBuilder.AppendLine("{");
            contentBuilder.AppendLine("    nodes = [");
            contentBuilder.AppendLine("        {");
            contentBuilder.AppendLine($"            type = \"point_text\"");
            contentBuilder.AppendLine($"            origin = \"{activeLineup.Coordinates.X} {activeLineup.Coordinates.Y} {activeLineup.Coordinates.Z}\"");
            contentBuilder.AppendLine($"            text = \"Lineup: {activeLineup.TargetZone} | {activeLineup.ThrowType}\"");
            contentBuilder.AppendLine("        }");
            contentBuilder.AppendLine("    ]");
            contentBuilder.AppendLine("}");

            // Overwrite cleanly using non-blocking stream methods
            await File.WriteAllTextAsync(OutputPath, contentBuilder.ToString(), Encoding.UTF8);
        }
    }
}