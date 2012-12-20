
select a.id,a.country from loan a, loan_lenders b, lender c where a.country = c.country_code limit 1000;

select a.lender_id,a.name from lender a where a.country_code is not null group by a.country_code;


select count(id),sector from loan where funded_date is not null group by sector;

select count(id),sector from loan where funded_date is null group by sector;

select count(id),country from loan where funded_date is null group by country;

select count(id),country from loan where funded_date is not null group by country;

select count(id), gender from loan where funded_date is null group by gender;

select count(id), gender from loan where funded_date is not null group by gender;

select count(lender_id) from lender where occupational_info is not null;

select count(id),activity from loan where funded_date is not null group by activity;

select count(id),activity from loan where funded_date is null group by activity;
	
select distinct activity,sector from loan order by sector;

select count(lender_id),country_code from lender where loan_count = 0 group by country_code;

select count(lender_id),country_code from lender where loan_count > 0 group by country_code;

