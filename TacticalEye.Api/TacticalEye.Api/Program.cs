using TacticalEye.Api.Services;
using TacticalEye.Api.Hubs;
using TacticalEye.Api.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSignalR();
builder.Services.AddScoped<ILineupRepository, DummyLineupRepository>();
builder.Services.AddScoped<IAnnotationWriter, AnnotationWriter>();

var app = builder.Build();

app.MapControllers();
app.MapHub<LineupHub>("/lineuphub");

app.MapGet("/", () => "TacticalEye API is running");

app.Run();
