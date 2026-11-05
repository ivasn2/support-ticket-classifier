package com.example.ticket_classifier.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "tickets")
public class Ticket {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String description;

    @ManyToOne
    @JoinColumn(name = "category_id", nullable = false) // указывает на имя колонки-внешнего ключа в таблице тикетов
    private Category category;

    // тут я сделал без классификации потому что если сервис упадет, то чтобы хотя бы сохранился без классификации
    private String sentiment; //перевод: тональность
    private Integer priority;

    private LocalDateTime createdAt = LocalDateTime.now(); //как только тикет появляется сразу у него дата
    private LocalDateTime answeredAt; //ТЗ (пункт 2.1): «Дата ответа — заполняется при обработке»

    @Enumerated(EnumType.STRING)
    private TicketStatus status = TicketStatus.NEW;

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public Category getCategory() {
        return category;
    }

    public String getSentiment() {
        return sentiment;
    }

    public Integer getPriority() {
        return priority;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getAnsweredAt() {
        return answeredAt;
    }

    public TicketStatus getStatus() {
        return status;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setCategory(Category category) {
        this.category = category;
    }

    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }

    public void setPriority(Integer priority) {
        this.priority = priority;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public void setAnsweredAt(LocalDateTime answeredAt) {
        this.answeredAt = answeredAt;
    }

    public void setStatus(TicketStatus status) {
        this.status = status;
    }
}
