// Yura Mamyrin

package net.yura.domination.engine.ai;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Vector;

import org.json.JSONObject;

import net.yura.domination.engine.core.Card;
import net.yura.domination.engine.core.Country;
import net.yura.domination.engine.core.Player;
import net.yura.domination.engine.core.RiskGame;

/**
 * THIS IS NOT A REAL AI, THIS IS WHAT A HUMAN PLAYER THAT HAS RESIGNED FROM A GAME BECOMES
 * SO THAT OTHER PLAYERS CAN CARRY ON PLAYING, THIS AI NEVER ATTACKS ANYONE, JUST FOLLOWS RULES
 * @author Yura Mamyrin
 */
public class AIEmulator implements AI {

    public int getType() {
        return Player.PLAYER_AI_EMULATOR;
    }

    public String getCommand() {
        return "emulator";
    }

    public void setGame(RiskGame game) {
        this.game = game;
        player = game.getCurrentPlayer();
    }

    protected Random r = new Random(); // this was always static

    protected RiskGame game;
    protected Player player;

    public String getBattleWon() {
    		String ans = "";
		int[] armies = getArmies();
		Country[] countries = game.getCountries();
		Country attacker = game.getAttacker();
		Country defender = game.getDefender();
		int[] x_state = new int[armies.length + countries.length + 1];
		for(int i = 0; i < armies.length; i++) {
			x_state[i] = armies[i];
		}
		for(int i = 0; i < countries.length; i++) {
			if(countries[i] == attacker) {
				x_state[i + armies.length] = 1;
			} else if(countries[i] == defender) {
				x_state[i + armies.length] = -1;
			} else {
				x_state[i + armies.length] = 0;
			}
		}
		x_state[x_state.length - 1] = game.getMustMove();
		try {
			ans = sendPost(5, x_state);
		} catch (Exception e) {
			e.printStackTrace();
		}
		if(ans.contains("\"")) {
			ans = ans.substring(1, ans.length() - 1);
		}
		return "move " + ans;
    }

    public String getTacMove() {
    		String ans = "";
		int[] armies = getArmies();
		try {
			ans = sendPost(6, armies);
		} catch (Exception e) {
			e.printStackTrace();
		}
		if(ans.contains("\"")) {
			ans = ans.substring(1, ans.length() - 1);
		}
		if(ans.equals("nomove")) {
			return ans;
		}
		return "movearmies " + ans;
    }

    public String getTrade() {

            List<Card> cards = player.getCards();

            if (cards.size() < 3) {
                    return "endtrade";
            }

            Card[] result = new Card[3];

            if (game.getBestTrade(cards, result) > 0) {
                    return getTrade(result);
            }

            return "endtrade";
    }

	protected String getTrade(Card[] result) {
		String output = "trade ";
		output = getCardName(result[0], output);
		output = output + " ";
		output = getCardName(result[1], output);
		output = output + " ";
		output = getCardName(result[2], output);
		return output;
	}

    private String getCardName(Card card1, String output) {
            if (card1.getName().equals("wildcard")) {
                    output = output + card1.getName();
            } else {
                    output = output + card1.getCountry().getColor();
            }
            return output;
    }

 // HTTP POST request
 	private String sendPost(int gameState, int[] x_state) throws Exception {
 		String url = "http://localhost:5000/api";
 		URL obj = new URL(url);
 		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

 		//add request header
 		con.setRequestMethod("POST");
 		con.setRequestProperty("Content-Type", "application/json");
 		con.setRequestProperty("Accept", "application/json");
 		con.setDoOutput(true);
 		con.setDoInput(true);
 
 		JSONObject state = new JSONObject();
 		state.put("gameState", gameState);
 		state.put("x_state", x_state);
 		
 		OutputStreamWriter wr = new OutputStreamWriter(con.getOutputStream());
 		wr.write(state.toString());
 		wr.flush();
 		wr.close();

 		int responseCode = con.getResponseCode();
 		System.out.println("\nSending 'POST' request to URL : " + url);
 		System.out.println("Post parameters : " + state.toString());
 		System.out.println("Response Code : " + responseCode);

 		BufferedReader in = new BufferedReader(
 		        new InputStreamReader(con.getInputStream()));
 		String inputLine;
 		StringBuffer response = new StringBuffer();

 		while ((inputLine = in.readLine()) != null) {
 			response.append(inputLine);
 		}
 		in.close();
 		
 		//print result
 		return response.toString();

 	}
 	
 	public int[] getArmies() {
		Country[] countries = game.getCountries();
		int[] armies = new int[countries.length];
		for(int i = 0; i < countries.length; i++) {
			if(countries[i].getOwner() == null) {
				armies[i] = 0;
			} else {
				armies[i] = countries[i].getOwner().getName().equals("Emulator") ? countries[i].getArmies() : -countries[i].getArmies();
			}
		}
		return armies;
 	}

    public String getPlaceArmies() {
    		Vector<String> commands = game.getCommands();
		String ans = "";
		int[] armies = getArmies();
		int[] x_state = new int[armies.length + 1];
		for(int i = 0; i < armies.length; i++) {
			x_state[i] = armies[i];
		}
		x_state[x_state.length - 1] = game.getCurrentPlayer().getExtraArmies();
		try {
			ans = sendPost(2, x_state);
		} catch (Exception e) {
			e.printStackTrace();
		}
		if(ans.contains("\"")) {
			ans = ans.substring(1, ans.length() - 1);
		}
		return "placearmies " + ans;
    }

    public String getAttack() {
    		String ans = "";
		int[] armies = getArmies();
		try {
			ans = sendPost(3, armies);
		} catch (Exception e) {
			e.printStackTrace();
		}
		if(ans.contains("\"")) {
			ans = ans.substring(1, ans.length() - 1);
		}
		if(ans.equals("endattack")) return ans;
		return "attack " + ans;
    }

    public String getRoll() {
    		Vector<String> commands = game.getCommands();
    		int[] armies = getArmies();
    		int[] x_state = new int[armies.length + 2];
    		for(int i = 0; i < armies.length; i++) {
    			x_state[i] = armies[i];
    		}
    		Country attacker = game.getAttacker();
    		Country defender = game.getDefender();
    		Country[] allCountries = game.getCountries();
    		for(int i = 0; i < allCountries.length; i++) {
    			if(allCountries[i] == attacker) {
    				x_state[x_state.length - 2] = armies[i];
    			} else if(allCountries[i] == defender) {
    				x_state[x_state.length - 1] = armies[i];
    			}
    		}
    		String ans = "";
    		try {
    			ans = sendPost(4, x_state);
    		} catch (Exception e) {
    			e.printStackTrace();
    		}
    		if(ans.contains("\"")) {
    			ans = ans.substring(1, ans.length() - 1);
    		}
    		if(ans.equals("retreat")) {
    			if(commands.get(commands.size() - 1).contains("attack")) { // To avoid infinite loops of attack and retreat, must be done here because Python server doesn't have access to prev commands
    				ans = "1";
    			} else {
        			return ans;
    			}
    		}
    		return "roll " + ans;
    }

    public String getCapital() {
	    return "capital " + randomCountry(player.getTerritoriesOwned()).getColor();
    }

    public Country randomCountry(List<Country> countries) {
    	if (countries.isEmpty()) {
    		return null;
    	}
    	return countries.get( r.nextInt(countries.size()) );
    }

    public String getAutoDefendString() {
		int[] armies = getArmies();
		int[] x_state = new int[armies.length + 2];
		for(int i = 0; i < armies.length; i++) {
			x_state[i] = armies[i];
		}
		Country attacker = game.getAttacker();
		Country defender = game.getDefender();
		Country[] allCountries = game.getCountries();
		for(int i = 0; i < allCountries.length; i++) {
			if(allCountries[i] == attacker) {
				x_state[x_state.length - 2] = armies[i];
			} else if(allCountries[i] == defender) {
				x_state[x_state.length - 1] = armies[i];
			}
		}
		String ans = "";
		try {
			ans = sendPost(10, x_state);
		} catch (Exception e) {
			e.printStackTrace();
		}
		if(ans.contains("\"")) {
			ans = ans.substring(1, ans.length() - 1);
		}
		return "roll " + ans;
    }
}
