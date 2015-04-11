
#include <assert.h>
#include <complex.h>
#include <ctype.h>
#include <errno.h>
#include <float.h>
#include <limits.h>
#include <locale.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>
#include <tgmath.h>
#include <time.h>
#include <uchar.h>
#include <wchar.h>
#include <wctype.h>

{% if not main %}
int main(int argc, const char **argv) {
{% endif %}
{{ code }}
{% if not main %}
	;
	return 0;
}
{% endif %}
