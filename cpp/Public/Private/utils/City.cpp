#include "City.h"
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using namespace pandemic;

// Constructor
City::City(std::string name, Color color, int population, float position[2])
	: name(std::move(name)), color(std::move(color)), population(population), research_station(false), outbroken(false), quarantined(false) {
	this->position[0] = position[0];
	this->position[1] = position[1];
}

// Accessor methods
std::string City::getName() {
	return name;
}

Color City::getColor() {
	return color;
}

bool City::hasResearchStation() {
	return research_station;
}

std::vector<City> City::getNeighbors() {
	return neighbors;
}

bool City::isOutbroken() {
	return outbroken;
}

bool City::isQuarantined() {
	return quarantined;
}

std::pair<float, float> City::getPosition() {
	return std::make_pair(position[0], position[1]);
}

// Action methods
void City::addNeighbor(City other) {
	neighbors.push_back(other);
}

void City::addDiseaseCubes(Color color, int num) {
	if (!quarantined) {
		int key = color.key;
		int curr = disease_cubes[key];

		if (num <= 0) {
			throw std::invalid_argument("Invalid number of cubes to add. Must add at least 1 cube");
		}
		if (num > 24) {
			throw std::invalid_argument("Too many cubes to add to " + name);
		}

		// too many cubes placed on city causes an outbreak
		if (curr + num > 3) {
			if (!outbroken) {
				disease_cubes[key] = 3;
				outbroken = true;
				outbreak();
			}
		}

		// normal cube add
		disease_cubes[key] += color.takeCubes(num);
	}
}

void City::removeDiseaseCubes(Color color, int num) {
	int key = color.key;
	int curr = disease_cubes[key];

	if (num <= 0) {
		throw std::invalid_argument("Invalid number of cubes to remove. Must remove at least 1 cube");
	}
	if (num > curr) {
		throw std::invalid_argument("Not enough cubes to remove from " + name);
	}

	disease_cubes[key] -= color.returnCubes(num);
}

void City::placeResearchStation() {
	research_station = true;
}

// Private method
void City::outbreak() {
	for (City& neighbor : neighbors) {
		neighbor.addDiseaseCubes(color, 1);
	}
}
