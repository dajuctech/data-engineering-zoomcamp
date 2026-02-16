{%- macro get_vendor_data(vendor_id) -%}
    case
        when {{ vendor_id }} = 1 then 'Creative Mobile Technologies, LLC'
        when {{ vendor_id }} = 2 then 'VeriFone Inc.'
        else 'Other'
    end
{%- endmacro -%}
