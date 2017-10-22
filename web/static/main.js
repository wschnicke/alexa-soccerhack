/* display message in list
*/
function message(homeTeam, awayTeam, gameTime, message, homeTeamScore=-1, awayTeamScore=-1) {
  var now = new Date();
  var teamInfo = (homeTeamScore == -1 || awayTeamScore == -1) ? `<b>${homeTeam}</b> - <b>${awayTeam}</b>` : `<b>${homeTeam}</b> (${homeTeamScore}) - <b>${awayTeam}</b> (${awayTeamScore})`;
  var message = `<span class='message'>[${now.getHours()}:${now.getMinutes()}] [${teamInfo}] ${gameTime ? gameTime + ' - ' : ''}${message}</span>`;
  $("#updates").append(message);
  return message;
}

/* socket handlers */
let socket = io();
socket.on("message", function(data) {
  message(data.homeTeam, data.awayTeam, data.gameTime, data.message, data.homeTeamScore, data.awayTeamScore);
});

/* fake data */
message("Columbus Crew", "Miami FC", "", "Game started!", 0, 0);
message("Columbus Crew", "Miami FC", "12'", "Keeper Zack Steffen scores a goal for Columbus Crew!", 1, 0);
