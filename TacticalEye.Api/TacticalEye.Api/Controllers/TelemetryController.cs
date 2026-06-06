using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;
using System.Linq;
using TacticalEye.Api.Models;
using TacticalEye.Api.Services;
using TacticalEye.Api.Hubs;

namespace TacticalEye.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TelemetryController : ControllerBase
    {
        private readonly ILineupRepository _repository;
        private readonly IAnnotationWriter _annotationWriter;
        private readonly IHubContext<LineupHub> _hubContext;

        public TelemetryController(ILineupRepository repository, IAnnotationWriter annotationWriter, IHubContext<LineupHub> hubContext)
        {
            _repository = repository;
            _annotationWriter = annotationWriter;
            _hubContext = hubContext;
        }

        [HttpPost("position")]
        public async Task<IActionResult> UpdatePosition([FromBody] RadarPositionUpdate update)
        {
            // 1. Math matching: Convert radar visual pixels into spatial boundaries
            var contextualLineups = await _repository.GetLineupsByProximityAsync(update.MapName, update.RadarX, update.RadarY);

            if (contextualLineups.Any())
            {
                // Action A: Instantly pipe visual payload over WebSockets to secondary monitor app
                await _hubContext.Clients.All.SendAsync("ReceiveActiveLineups", contextualLineups);

                // Action B: Dynamically overwrite the CS2 native engine annotation script file
                await _annotationWriter.WriteNativeAnnotationFileAsync(contextualLineups.First());
            }

            return Ok(new { status = "Processed", detectedCount = contextualLineups.Count });
        }
    }
}