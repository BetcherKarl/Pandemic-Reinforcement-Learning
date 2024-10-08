#include <string>

namespace pandemic {

	abstract class Card {
	public:
		string getName() { return name; }
		virtual void use() = 0;

	private:
		string name;
	};

	class InfectionCard : public Card {
	public:
		InfectionCard(City c) {
			city = c;
			name = c.getName();
		}

		void use() {
			city.addDiseaseCubes(city.getColor(), 1);
		}

	private:
		City city;
	};

	abstract class PlayerCard : public Card {};

	class CityCard : public PlayerCard {
	public:
		Color getColor() { return city.getColor(); }

		CityCard(City c) {
			city = c;
			name = c.getName();
		}
	private:
		City city;
	};

}
	
