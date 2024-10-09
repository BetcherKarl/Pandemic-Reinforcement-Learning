#include "Color.h"

namespace pandemic {

	// Constructor
	Color::Color(std::string name) {
		this->name = name;
		this->disease_cubes = 24;
		this->cured = 0;
	}

	// Accessor methods
	bool Color::isCured() const {
		return cured >= 1;
	}

	bool Color::isEradicated() const {
		return cured == 2;
	}

	int Color::getDiseaseCubes() const {
		return disease_cubes;
	}

	std::string Color::getName() const {
		return name;
	}

	// Action methods
	void Color::cure() {
		if (cured == 0) {
			setCured(1);
		}
		if (disease_cubes == 24) {
			setCured(2);
		}
	}

	void Color::eradicate() {
		if (cured == 1 && disease_cubes == 24) {
			setCured(2);
		}
	}

	int Color::takeCubes(int num) {
		if (num <= 0) {
			throw std::invalid_argument("Invalid number of cubes to take. Must take at least 1 cube");
		}
		if (num > disease_cubes) {
			throw std::invalid_argument("Not enough cubes to take. Game Lost.");
		}
		disease_cubes -= num;
		return num;
	}

	int Color::returnCubes(int num) {
		if (num <= 0) {
			throw std::invalid_argument("Invalid number of cubes to return. Must return at least 1 cube");
		}
		if (disease_cubes + num > 24) {
			throw std::invalid_argument("Too many cubes to return");
		}

		disease_cubes += num;
		return num;
	}

	// Private helper method
	void Color::setCured(int cured) {
		if (cured < 0 || cured > 2) {
			throw std::invalid_argument(std::format("Invalid value cured ({}) for setCured().", cured));
		}
		this->cured = cured;
	}
}
