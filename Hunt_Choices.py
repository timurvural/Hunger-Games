from __future__ import division
slackerfest=False
## Determines whether or not I will always slack this round.
suckerlist=[]
## List of players who will hunt with me regardless of the decisions I made
## last round.
last_reps=[]
## List of reputations from the last round
huntslack=[]
## The decision (hunt or slack) each player made against me last round. In
## the same order as last_reps.
total_decisions=0
## The number of times any player has decided to hunt or slack in the entire game.
last_hunts=0
## The value of number_hunters last round.
unfriendliness=0
## Number of consecutive rounds that people hunted against me with less than
## the average probability.
def hunt_choices(
                round_number,
                current_food,
                current_reputation,
                m,
                player_reputations,
                ):
       
    import random
    hunt_decisions=[]
    new_suckers=[]
## Updates the indices of the "suckers" that were identified last round.
    global suckerlist
    global slackerfest
    global huntslack
    global last_reps
    global total_decisions
    global last_hunts
    global unfriendliness
    b=len(last_reps)
    avg=last_hunts/(b+1)
## Average number of times an arbitrary player was hunted against last round.
    friends=0
    for x in huntslack:
        if x=='h':
           friends+=1 
## "friends" is the number of times I was hunted against last round.
    if avg>friends:
        Be_More_Friendly=True
        unfriendliness+=1
        
    else:
        Be_More_Friendly=False
        unfriendliness=0
    if round_number<=2:
        for x in player_reputations:
            hunt_decisions.append('h')
##  Always hunt in the first two rounds to signal to other players that
##  you are willing to cooperate.                  

    elif len(player_reputations)==1:
        hunt_decisions.append('s')
##  Both players at the end of the game will be playing to win, so the optimal
##  strategy is to always slack, since there are no other players to deal with.

    else:
        for x in player_reputations:
            hunt_decisions.append(' ')
        restart=1
        possible_indices=[]
        for j in range(0,len(last_reps)):
            possible_indices.append(j)
## Every time a reputation from last round is uniquely matched with a reputation from
## this round, that reputation is deleted from the list of possible reputations
## and the matching process restarts. This continues until no more
## unique matches can be made.
        while restart>0:
            for x in range(0,len(player_reputations)):
                restart=0
                matches=[]
## For each player x, matches is the list of reputations from last round that could match
## up with x's reputation this round.
                
                for index in possible_indices:
                    v=player_reputations[x]*(total_decisions)-last_reps[index]*(total_decisions-len(player_reputations))
## v is the number of times player x would have to have hunted last round if
## x had reputation y at the start of the last round. If v satisfies the
## inequality below, it is possible that player x started last round with
## reputation y.
                    if 0<=v<=len(player_reputations):
                        matches.append(index)
                if player_reputations[x]>0.93 or 0.1>player_reputations[x]:
                    if round_number>2:
                        hunt_decisions[x]='s'
## If a player hunts too much or too little of the time, he is probably not
## taking my decisions into consideration, so the best option is to slack.                  

                elif len(matches)==1:
                    restart+=1
                    hunt_decisions[x]=huntslack[matches[0]]
                    possible_indices.remove(matches[0])
                    if matches[0] in suckerlist:
                        new_suckers.append(x)
## If a player from this round is identified as being the same player from
## a previous round, it can be determined whether said player was a sucker
## last round.
                elif len(matches)==0:
                    pass
## If it can be determined what decision a player made against me last round,
## I will make the same decision against him.                         
                            
                else:
## If it cannot be determined what my opponent did last round, I need a new
## strategy.
                    h=[]
                    for y in player_reputations:
                        h.append(y)
                    h.remove(player_reputations[x])
                    h.append(current_reputation)
                    h.sort()
## Creates a sorted list of the reputations that player x would be passed.
                    intrep=int(player_reputations[x]*len(player_reputations))
## If player x has reputation r, he/she must hunt on average r*len(player_reputations)
## to maintain that reputation. I am estimating that, therefore, player x
## always hunts against the top int(r*len(player_reputations)) reputations
## and hunts with probability {r*len(player_reputations} against the next best
## reputed player after that. If I estimate that player x will hunt against me,
## I will hunt against him/her.                   
                    if intrep>0:
                        if current_reputation>=h[len(h)-intrep]:
                            hunt_decisions[x]=('h')
                        elif current_reputation==h[len(h)-1-intrep]:
                            if random.random()<player_reputations[x]*len(player_reputations)-intrep:
                                hunt_decisions[x]=('h')
                            else:
                                hunt_decisions[x]=('s')
                        else:
                            hunt_decisions[x]=('s')
                    else:
                        hunt_decisions[x]=('s')
    suckerlist=new_suckers
    if Be_More_Friendly==True and round_number>2:
        for x in range(0,len(hunt_decisions)):
            if random.random()<max(player_reputations) and random.random()<0.01*unfriendliness and 0.1<=player_reputations[x]<=0.93:
                hunt_decisions[x]='h'
    else:
        for x in range(0,len(hunt_decisions)):
            if random.random()<0.01:
                hunt_decisions[x]='h'
## There is a chance of an arbitrary slack decision to be made a hunt decision.
## This chance is bounded by both the maximum reputation in the game and the
## number of consecutive rounds in which I have hunted against more than the
## average player. This can help break viscious circles in which I always slack
## with an opponent and the opponent always slacks with me.

    if slackerfest==True:
        for x in range(0,len(hunt_decisions)):
            hunt_decisions[x]='s'
        slackerfest=False
    elif random.random()<5/round_number and round_number>2*len(player_reputations):
        slackerfest=True
        for x in range(0,len(hunt_decisions)):
            hunt_decisions[x]='s'
    else:
        slackerfest=False
        for q in range(0, len(player_reputations)):
            if q in suckerlist:
                hunt_decisions[q]='s'
            
## This is a mechanism to take advantage of bad algorithms. After a large number
## of rounds, my reputation changes very little based on the results of one
## individual round. If an opposing algorithm takes into account only my
## reputation, their decision against me should not change based on the results
## of one round, and so I should slack against them until they stop hunting
## with me. Slackfests are less likely as the game progresses.

    total_decisions+=len(player_reputations)
    last_reps=player_reputations    
    return (hunt_decisions)

def hunt_outcomes(food_earnings):
    global huntslack
    global slackerfest
    global suckerlist
    huntslack=[]
    for x in food_earnings:
        if x>-1:
            huntslack.append('h')
        else:
            huntslack.append('s')
    if slackerfest==True:
        suckerlist=[]
        for x in range(0, len(food_earnings)):
            suckerlist.append(x)
    else:
        for x in range(0, len(food_earnings)):
            if food_earnings[x]<-1 and x in suckerlist:
                suckerlist.remove(x)
def round_end(award, m, number_hunters):
    global last_hunts
    last_hunts=number_hunters
