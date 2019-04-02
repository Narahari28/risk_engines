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
	return "move all";
    }

    public String getTacMove() {
	return "nomove";
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

    public String getPlaceArmies() {
		Country[] countries = game.getCountries();
		int[] armies = new int[countries.length];
		String ans = "";
		for(int i = 0; i < countries.length; i++) {
			if(countries[i].getOwner() == null) {
				armies[i] = 0;
			} else {
				armies[i] = countries[i].getOwner().getName().equals("Emulator") ? countries[i].getArmies() : -countries[i].getArmies();
			}
		}
		try {
			ans = sendPost(2, armies);
			System.out.println(ans);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return "placearmies " + ans + " 1";
    }

    public String getAttack() {
    	return "endattack";
    }

    public String getRoll() {
	return "retreat";
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
        int n=game.getDefender().getArmies();
        return "roll "+Math.min(game.getMaxDefendDice(), n);
    }

	protected String getPlaceCommand(Country country, int armies) {
		return "placearmies " + country.getColor() + " " + (!game.getSetupDone()?1:Math.max(1, Math.min(player.getExtraArmies(), armies)));
	}

}
