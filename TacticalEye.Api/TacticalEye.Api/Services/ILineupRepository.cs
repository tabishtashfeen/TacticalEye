using System.Collections.Generic;
using System.Threading.Tasks;
using TacticalEye.Api.Models;

namespace TacticalEye.Api.Services
{
    public interface ILineupRepository
    {
        Task<List<LineupModel>> GetLineupsByProximityAsync(string mapName, int radarX, int radarY);
    }
}
