namespace pandemic {
	class Color {
		public:
			int key;

			Color(string name) {
				this->name = name;
				this->disease_cubes = 24;
				this->cured = 0;
			}

			void cure() {
				if (cured == 0) {
					set_cured(1);
				}
				if (disease_cubes == 24) {
					set_cured(2);
				}
			}

			void eradicate() {
				if (cured == 1) {
					set_cured(2);
				}
			}

			int takeCubes(int num) {
				if (num <= 0) {
					throw invalid_argument("Invalid number of cubes to take. Must take at least 1 cube");
				}
				if (num > disease_cubes) {
					throw invalid_argument("Not enough cubes to take from " + name + ". Game Lost.");
				}
				disease_cubes -= num;
				return num;
			}

			int returnCubes(int num) {
				if (num <= 0) {
					throw invalid_argument("Invalid number of cubes to return. Must return at least 1 cube");
				}
				if (disease_cubes + num > 24) {
					throw invalid_argument("Too many cubes to return to " + name);
				}

				disease_cubes += num;
				return num;
			}

		private:
			string name;
			int disease_cubes; // Number of disease cubes left for this color
			int cured; // 0 for uncured, 1 for cured, 2 for eradicated

			void set_cured(int cured) {
				if (cured < 0 || cured > 2) {
					throw invalid_argument("Invalid value for cured");
				}
				this->cured = cured;
			}
	};
}
