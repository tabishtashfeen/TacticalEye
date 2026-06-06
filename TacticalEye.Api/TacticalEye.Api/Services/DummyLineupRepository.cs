using System.Collections.Generic;
using System.Threading.Tasks;
using TacticalEye.Api.Models;

namespace TacticalEye.Api.Services
{
    public class DummyLineupRepository : ILineupRepository
    {
        public Task<List<LineupModel>> GetLineupsByProximityAsync(string mapName, int radarX, int radarY)
        {
            return Task.FromResult(new List<LineupModel>());
        }
    }
}
