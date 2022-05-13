Select Waiter_ID, Name, Birthday, Address, Date_In, Date_Out from restaurant.waiter
left join (Select * from restaurant.order where year(Order_Date_Time) = $sql_val2 and month(Order_Date_Time) = $sql_val1) sel1
using (Waiter_ID)
where Order_ID is NULL;