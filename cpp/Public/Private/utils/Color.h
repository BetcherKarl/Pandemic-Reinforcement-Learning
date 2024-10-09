#ifndef COLOR_H
#define COLOR_H

#include <string>
#include <stdexcept>
#include <format>

namespace pandemic {

    class Color {
    public:
        int key;

        // Constructor
        Color(std::string name);

        // Accessor methods
        [[nodiscard]] bool isCured() const;
        [[nodiscard]] bool isEradicated() const;
        [[nodiscard]] int getDiseaseCubes() const;
        [[nodiscard]] std::string getName() const;

        // Action methods
        void cure();
        void eradicate();
        int takeCubes(int num);
        int returnCubes(int num);

    private:
        std::string name;
        int disease_cubes; // Number of disease cubes left for this color
        int cured; // 0 for uncured, 1 for cured, 2 for eradicated

        // Helper method
        void setCured(int cured);
    };

}

#endif // COLOR_H
