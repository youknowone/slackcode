
#include <cassert>
#include <ccomplex>
#include <cctype>
#include <cerrno>
#include <cfloat>
#include <climits>
#include <clocale>
#include <cstdbool>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <ctgmath>
#include <ctime>
#include <cwchar>
#include <cwctype>

#include <array>
#include <bitset>
#include <deque>
#include <forward_list>
#include <list>
#include <map>
#include <queue>
#include <set>
#include <stack>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <algorithm>
#include <chrono>
#include <functional>
#include <iterator>
#include <memory>
#include <stdexcept>
#include <tuple>
#include <utility>
#include <locale>
#include <string>
#include <regex>
#include <fstream>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <ostream>
#include <sstream>
#include <streambuf>
#include <exception>
#include <limits>
#include <new>
#include <typeinfo>
#include <complex>
#include <random>
#include <valarray>
#include <numeric>


{% if not main %}
int main(int argc, const char **argv) {
{% endif %}
{{ code|safe }}
{% if not main %}
	;
	return 0;
}
{% endif %}
