clear
import excel using "C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_total_cities.xlsx", firstrow

*create region_num 
encode region, generate(region_num)
*drop nan values
keep if GDP != .
keep if guilds_nr_region !=. 

*calculate regression evaluating the impact of guilds number on GDP
reg GDP_city guilds_nr_region i.year

clear
import excel using "C:\Users\edobo\OneDrive\Desktop\Thesis\Medieval Guilds\Data\EDITED_db\pil\pil_attempt_total_cities.xlsx", firstrow


*create lagged variable
sort region_num group 
by region_num: gen lag1 = region_new_guilds[_n-1]
encode region, generate(region_num)
xtset region_num group


