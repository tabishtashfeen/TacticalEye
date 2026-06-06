namespace TacticalEye.Api.Models
{
    public class LineupModel
    {
        public Coordinates Coordinates { get; set; }
        public string TargetZone { get; set; }
        public string ThrowType { get; set; }
    }

    public class Coordinates
    {
        public float X { get; set; }
        public float Y { get; set; }
        public float Z { get; set; }
    }
}
