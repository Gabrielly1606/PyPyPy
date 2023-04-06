class RPGFormulas:
    @staticmethod
    def calculate_damage(attacker_level, attacker_attack, defender_defense):
        """
        Calculates the damage dealt by an attacker to a defender.

        Args:
            attacker_level (int): The level of the attacker.
            attacker_attack (int): The attack stat of the attacker.
            defender_defense (int): The defense stat of the defender.

        Returns:
            int: The amount of damage dealt by the attacker.
        """
        damage = (2 * attacker_level + 10) / 250 * (attacker_attack / defender_defense) + 2
        return int(damage)

    @staticmethod
    def calculate_experience(level, base_experience):
        """
        Calculates the amount of experience required to reach the next level.

        Args:
            level (int): The current level factor of the character.
            base_experience (int): The amount of experience required to reach level 1.

        Returns:
            int: The amount of experience required to reach the next level.
        """
        #experience = base_experience // level/2
        #level = base_experience / 100 / 1.5
        experience = base_experience * level * 1.5
        return int(experience)
    
    @staticmethod
    def calculate_level(total_exp, factor, base_exp):
        level = 1
        required_exp = base_exp * factor
        while total_exp >= required_exp:
            level += 1
            total_exp -= required_exp
            required_exp = base_exp * (level ** factor)
        return level
    
    @staticmethod
    def calculate_hit_chance(attacker_accuracy, defender_evasion):
        """
        Calculates the chance of an attacker hitting a defender.

        Args:
            attacker_accuracy (int): The accuracy stat of the attacker.
            defender_evasion (int): The evasion stat of the defender.

        Returns:
            float: The chance of the attacker hitting the defender (between 0 and 1).
        """
        hit_chance = attacker_accuracy / (attacker_accuracy + defender_evasion)
        return round(hit_chance, 2)

    @staticmethod
    def calculate_stat_increase(level, base_stat):
        """
        Calculates the amount of increase in a stat per level.

        Args:
            level (int): The current level of the character.
            base_stat (int): The base stat value at level 1.

        Returns:
            int: The amount of increase in the stat per level.
        """
        stat_increase = base_stat * (level / 50)
        return int(stat_increase)
