/* message function:
  team A, team B, team A score, team B score, game time, message
*/
function message(teamA, teamB, teamAScore, teamBScore, gameTime, msg) {
  var now = new Date();
  var message = `<span class='message'>[${now.getHours()}:${now.getMinutes()}] [<b>${teamA}</b> (${teamAScore}) - <b>${teamB}</b> (${teamBScore})] ${gameTime ? gameTime + ' - ' : ''}${msg}</span>`;
  $("#updates").append(message);
  return message;
}

/* socket handlers */
let socket = io();
socket.on("message", function(data) {
  message(data.teamA, data.teamB, data.teamAScore, data.teamBScore, data.gameTime, data.msg);
});

/* fake data */
message("Columbus Crew", "Miami FC", 0, 0, "", "Game started!");
message("Columbus Crew", "Miami FC", 1, 0, "12'", "Keeper Zack Steffen scores a goal for Columbus Crew!");
