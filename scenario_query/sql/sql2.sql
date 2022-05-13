Select Waiter_ID, Name, count(*) as order_kol, sum(Order_Cost) as order_sum from restaurant.waiter
join (Select * from restaurant.order
where year(Order_Date_Time) = $sql_val2 and month(Order_Date_Time) = $sql_val1) sel1
using (Waiter_ID)
group by Name, Waiter_ID;