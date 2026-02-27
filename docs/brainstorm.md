# Valuing a balls outcome vs the expected outcome

### Stage of game

- Runs are easier to get in the powerplay
  - Therefore batters should be rewarded less and bowlers rewarded more for low outcome balls

Options:
- Compare player impact at a match level
- At a season level
- At a ground level
- Or cross
- Benefits / Pitfalls
  - Match Level
    - Can be directly compared to others players performances in the same game
    - Takes away from bowler performance in games where one team gets bowled out for very few runs and opposition chases it down quickly
  - Potential Solutions:
    - Each game can be won or lost
      - Therefore each game has one win available. Every act contributes towards a teams chance of winning or losing
      - In a game where a team gets bowled out for 60 in 10 overs and the opposition chases it down in 10.1 overs making 61 for no wickets. No extras were conceded
      - For each ball:
      - $$ E(runs) = (runs_{team one}+runs_{team two})/(balls_{team one} + balls_{team two}) $$
      - Meaning
        - $$ E(runs) = (60+61)/(60+61) = 121/121 = 1$$
        - In this case, only a dot or dismissal is a negative event for each batsman, to calculate the value of a wicket we use the following formula
        - $$ value(dismissal) = (runs_{team one} + runs_{team two} -all_{extras}) / (wickets_{team one} + wickets_{team two}) $$
        - $$ Value(dismissal) = (60+61) / (10) = 121/10 = 12.1 $$
   -  Next question
      -  Now that we have a method to derive value for each ball and outcome, how should extras be valued and how should runouts be credited?
      -  According the formula
      -  $$ Total(runs) = (runs_{team one} + run_{team two} - all(extras)) $$
         -  Batter should not get any credit for a bowler bowling an extra, this means that a model can be derived for a batter but not bowler as of yet.
-  After the value of each outcome is calculated for each match, the next steps are:
   -  Give all players the same elo rating at start ~1500.
   -  Then utilise equation for each matchup and each outcome. Run method for all t20 matches.
-  $$Val(Wicket) = E(runs_{before}) - E(runs_{after}) $$
-  $$E(runs) = (E(extras_{ball}) + E(runs_{ball}))