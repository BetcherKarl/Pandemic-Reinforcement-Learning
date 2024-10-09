namespace pandemic {
    #include <string>
    #include <vector>
    #include <unordered_map>
    #include <functional>
    using namespace std;

    abstract class Player {
    public:
        virtual string pawnColor() = 0;
        virtual string getRole() = 0;

        Player(City startingLocation) {
            this->score = 0;
            this->action_count = 0;
            this->action_limit = 4;
            this->hand_limit = 7;
            this->cards_to_cure = 5;
            this->location = startingLocation;
            actions[""]
        }

        void addToHand(PlayerCard c) {
            if (hand.size() => hand_limit) {
                invalid_argument("Hand is full");
            }

            hand.push_back(c);
        }

        int discoverACure() {
            if (this.location.hasResearchStation) {
                // count the number of cards for each color in the players hand
                // verify they can cure the disease
                // cure the disease color
                // check for win state
            }
        }
    private:

        int score;
        int action_limit;
        int action_count;
        int hand_limit;
        int cards_to_cure;
        vector<PlayerCard> hand;
        City location;
        unordered_map<string, function<int>> actions;
    };

}