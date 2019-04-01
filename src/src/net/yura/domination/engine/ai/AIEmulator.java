// Yura Mamyrin

package net.yura.domination.engine.ai;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.List;
import java.util.Random;

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

    public String performGetRequest() {
			String USER_AGENT = "Mozilla/5.0";
		String url = "http://www.google.com/search?q=java";

		URL obj = null;
		try {
			obj = new URL(url);
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		HttpURLConnection con = null;
		try {
			con = (HttpURLConnection) obj.openConnection();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		// optional default is GET
		try {
			con.setRequestMethod("GET");
		} catch (ProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		//add request header
		con.setRequestProperty("User-Agent", USER_AGENT);

		int responseCode = 0;
		try {
			responseCode = con.getResponseCode();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("\nSending 'GET' request to URL : " + url);
		System.out.println("Response Code : " + responseCode);

		BufferedReader in = null;
		try {
			in = new BufferedReader(
			        new InputStreamReader(con.getInputStream()));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String inputLine;
		StringBuffer response = new StringBuffer();

		try {
			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			in.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return response.toString();
    }

    public String getPlaceArmies() {
		Country[] countries = game.getCountries();
		Integer[] armies = new Integer[countries.length];
		for(int i = 0; i < countries.length; i++) {
			if(countries[i].getOwner() == null) {
				armies[i] = 0;
			} else {
				armies[i] = countries[i].getOwner().getName().equals("Emulator") ? countries[i].getArmies() : -countries[i].getArmies();
			}
		}
		System.out.println(performGetRequest());
		return "autoplace";
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
