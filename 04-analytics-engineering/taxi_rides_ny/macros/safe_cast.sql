{%- macro safe_cast(column_name, new_type) -%}
    {% if target.type == 'bigquery' %}
        safe_cast({{ column_name }} as {{ new_type }})
    {% else %}
        try_cast({{ column_name }} as {{ new_type }})
    {% endif %}
{%- endmacro -%}
