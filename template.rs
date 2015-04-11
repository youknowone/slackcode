
#[allow(unused_imports)]
use std::*;

{% if not main %}
fn main() {
{% endif %}
{{ code }}
{% if not main %}
}
{% endif %}
