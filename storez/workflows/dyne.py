<<<<<<< HEAD
def createFoodCategory(restaurant, category_name, description):
    try:
        category = FoodCategory.objects.create(
            id=uuid.uuid4().hex[:8].upper(),
            restaurant=restaurant,
            category_name=category_name,
            description=description
        )

        return category
    except Exception as e:
        logger.error("createCategory@Error : : Error occured while creating category")
        logger.error(e)
        return None


def getCategoryById(categoryId):