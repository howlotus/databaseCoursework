Select Dish_ID, Dish_Name, sum(Dish_Quantity) as dish_sum, sum(Dish_Quantity)*Dish_Price as month_result from restaurant.dish
join (restaurant.order_line
join (Select * from restaurant.order
where year(Order_Date_Time) = $sql_val2 and month(Order_Date_Time) = $sql_val1) sel1
using (Order_ID))
using (Dish_ID)
group by Dish_ID, Dish_Name;