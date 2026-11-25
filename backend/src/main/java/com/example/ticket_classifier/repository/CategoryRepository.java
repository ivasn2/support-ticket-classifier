package com.example.ticket_classifier.repository;

import com.example.ticket_classifier.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<Category,Long> {
}
