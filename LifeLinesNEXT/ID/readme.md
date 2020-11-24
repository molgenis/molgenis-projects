# ID's for LifeLines NEXT

NEXTnumbers are the key to materials and participants, therefore checks on validity of IDs are needed, a list of IDs that can't be mistyped and a system that sees to it that IDs are unique between participants.

* [11- proof](/LifeLinesNEXT/ID/11_proof.xlsx) (empty excel with function to check ID)
* [Schematic](https://github.com/molgenis/molgenis-projects/blob/master/LifeLinesNEXT/ID/issues%20ID_NEXT.pdf) view on IDs. With nightly mapping IDs in different tables can not be reused, so all NEXT numbers are unique.
* Validation expression used:
```
expression NEXT_baby() {
$('next_nr_baby').matches(/^[0-9]{6}$/i).value()
}
```
Check if ID has ONLY digits and only variety of 6 digits can be used.

![NEXT_ID_model](/LifeLinesNEXT/ID/nummers.png)
