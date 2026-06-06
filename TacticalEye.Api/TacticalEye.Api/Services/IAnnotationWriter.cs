using System.Threading.Tasks;
using TacticalEye.Api.Models;

namespace TacticalEye.Api.Services
{
    public interface IAnnotationWriter
    {
        Task WriteNativeAnnotationFileAsync(LineupModel activeLineup);
    }
}
