#ifndef CITY_H
#define CITY_H

#include <string>
#include <vector>
#include "Color.h"

namespace pandemic {

    class City {
    private:
        std::string name;
        Color color;
        int population;
        bool research_station;
        std::vector<City> neighbors;
        bool outbroken;
        bool quarantined;
        float position[2];
        std::vector<int> disease_cubes; // The number of disease cubes for each color, stored by index from Color Object

        // Helper method
        void outbreak();

    public:
        // Constructor
        City(std::string name, Color color, int population, float position[2]);

        // Accessor methods (getters)
        std::string getName();
        Color getColor();
        bool hasResearchStation();
        std::vector<City> getNeighbors();
        bool isOutbroken();
        bool isQuarantined();
        std::pair<float, float> getPosition();

        // Action methods
        void addNeighbor(City other);
        void addDiseaseCubes(Color color, int num);
        void removeDiseaseCubes(Color color, int num);
        void placeResearchStation();
    };
}

#endif // CITY_H